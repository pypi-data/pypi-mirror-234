"""
Skulk.

A tool to help get your repo in good shape for a release.

It works for packages intended for PyPi.

It has 2 public functions:

1. main() : A wizard that guides you to choosing a version that does not conflict with any git tags
   or PyPi versions.

If no pre-push hook exists in the repo, skulk will prompt and help to make one.

2. run_pre_push_checks() : A function that is designed to be called from a git pre-push hook.

Assumptions: 1. You have a file named VERSION at the top level of the repo. It should contain a
simple semver such as 1.2.3 2. You have a CHANGELOG.md  at the top level of the repo.


WIZARD MESSAGES:

1. Nothing will happen until the end. You can exit at any time.
2. Do you want to simply push your code(0), deploy a pre-release(1), or deploy a release(2)?
3. If pre-release(1) or release(2):
    a. You'll be shown the current version and the latest version on PyPi.
    b. You'll be asked to choose a new version from the options.


"""

from __future__ import print_function
import datetime
import os
import sys
from skulk import util
from skulk.bumper import (
    Bumper,
    RELEASE_SCOPE_BETA,
    RELEASE_SCOPE_CANDIDATE,
    RELEASE_SCOPE_RELEASE,
)

from tabulate import tabulate

# Termios is not available on Windows, so we use our own homegrown, less elegant, solution.
try:
    from skulk import questions as q
except (ImportError, ModuleNotFoundError):
    from skulk import questions_fallback as q



class Skulk(object):
    """A wizard to guide the user to a good version and changelog."""

    def __init__(self):
        self.repo = util.get_repo()
        self.branch = self.repo.active_branch
        self.branch_name = self.branch.name
        self.working_dir = self.repo.working_dir
        self.hook_filename = os.path.join(self.working_dir, ".git", "hooks", "pre-push")
        self.changelog_filename = os.path.join(self.working_dir, "CHANGELOG.md")
        self.version_filename = os.path.join(self.working_dir, "VERSION")
        self.pip_name = util.get_pip_name(self.repo)
        self.bumper = None
        self.edit_changelog = False
        self.changelog_addition = ""
        self.release_scope = None
        self.next_version = None

    def run(self):
        self.check_pre_push_hook()
        self.bumper = Bumper(self.repo, self.pip_name)
        self.check_clean()
        self.release_scope = self.ask_release_scope()
        self.show_recent_versions()
        self.next_version = self.ask_version()
        self.ask_changelog_update()
        self.write_version()
        self.commit_version_changelog()
        tag = self.add_tag()
        self.ask_push(tag)
        sys.exit(0)

    def check_clean(self):
        """Check that the repo is clean and give user a chance to clean it up.

        User can continue with a dirty repo, but we at least want to warn about it.
        """
        if not self.repo.is_dirty():
            print(util.green("Repo clean. Good to go."))
            return

        print(util.red("Attention: Repository is dirty."))

        mods = [item.a_path for item in self.repo.index.diff(None)]
        util.print_truncated_list(
            mods,
            "Modified files",
            header_color=util.magenta,
            item_color=util.default_color,
        )

        untracked = self.repo.untracked_files
        util.print_truncated_list(
            untracked,
            "Untracked files",
            header_color=util.blue,
            item_color=util.default_color,
        )

        q.wait("If you want to include them, please commit them now.")

    def ask_release_scope(self):
        prompt = "What kind of deployment do you want to make?"
        choices = [
            {"label": "Beta release for internal testing", "value": RELEASE_SCOPE_BETA},
            {
                "label": "Candidate release for customer testing",
                "value": RELEASE_SCOPE_CANDIDATE,
            },
        ]
        if self.branch_name == "master":
            choices.append({"label": "Full release", "value": RELEASE_SCOPE_RELEASE})
        return q.choose(prompt, choices)

    def show_recent_versions(self):
        versions_table = self.bumper.versions_table()
        print(
            util.yellow(
                "Here's a table of recent versions on PyPi and in the repository"
            )
        )
        print(
            tabulate(
                versions_table, headers="firstrow", tablefmt="pretty", stralign="left"
            )
        )
        print("\n")

    def ask_version(self):
        choices = self.bumper.version_options(release_scope=self.release_scope)
        choices.append({"label": "Custom (Not recommended)", "value": "custom"})
        choice = q.choose(
            f"What {self.release_scope} version do you want to deploy?", choices
        )

        if choice == "custom":
            if self.release_scope == RELEASE_SCOPE_BETA:
                validator = self.bumper.validate_beta_version
            elif self.release_scope == RELEASE_SCOPE_CANDIDATE:
                validator = self.bumper.validate_candidate_version
            else:
                validator = self.bumper.validate_release_version

            choice = q.input_string(
                f"Enter a valid {self.release_scope} version number:",
                validator=validator,
            )

        return choice

    def ask_changelog_update(self):
        """Generate the reference additions to the changelog.

        Do not write anything to the changelog file yet."""

        changelog_update = True
        stub = ""
        if self.release_scope == RELEASE_SCOPE_BETA:
            print(
                util.yellow(
                    "Since this is an internal beta release, an updated changelog is optional."
                )
            )
            changelog_update = q.yes_no("Do you want to update the changelog?")
            if self.changelog_needs_unreleased_stub():
                stub = f"## Unreleased: \n\n"
        else:
            date_string = datetime.date.today().strftime("%d %b %Y")
            stub = f"## Version:{self.next_version} -- {date_string}\n\n"

        if changelog_update:
            terminal_advice = util.yellow(
                "Here are some recent commit message for reference:\n"
            )
            terminal_advice += "-" * 30 + "\n"
            commits = util.get_recent_commits(self.repo)
            commit_messages = [f"* {c.summary}" for c in commits]
            terminal_advice += "\n".join(commit_messages)
            terminal_advice += "\n"

            print(terminal_advice)

            if stub:
                with open(self.changelog_filename, "r", encoding="utf-8") as clog:
                    content = clog.read() or "--"

                content = stub + "\n\n" + content

                with open(self.changelog_filename, "w", encoding="utf-8") as clog:
                    clog.write(content)

            q.wait(
                "Please EDIT and SAVE your CHANGELOG now. (There's no need to commit)"
            )

    def changelog_needs_unreleased_stub(self):
        """Return True if the changelog needs an unreleased stub."""
        with open(self.changelog_filename, "r", encoding="utf-8") as f:
            datafile = f.readlines()

        for line in datafile:
            if line.startswith("## Unreleased"):
                return False
            elif line.startswith("## Version"):
                return True
        return True

    def write_version(self):
        """Write the new version number to the appropriate file."""
        with open(self.version_filename, "w", encoding="utf-8") as vfn:
            vfn.write(self.next_version)

        # PRIVATE

    def ask_push(self, tag):
        """Ask the user if he wants to push the branch and tag."""
        do_push = q.yes_no(
            f"Do you want me to push the current branch and tag? ({self.branch_name}/{tag.name})"
        )

        origin = self.repo.remote("origin")
        if do_push:
            origin.push(self.branch)
            origin.push(tag)
            print("Pushed branch and tag.\n")
        else:
            print(
                util.yellow(
                    "No worries. Use the following command to push later. Bye\n"
                )
            )
            print(util.green(f"git push --atomic origin {self.branch_name} {tag.name}"))

    def add_tag(self):
        """Add a tag to the repo."""
        if self.release_scope == RELEASE_SCOPE_BETA:
            label = "Pre-release"
        elif self.release_scope == RELEASE_SCOPE_CANDIDATE:
            label = "Release candidate"
        else:
            label = "Release"

        tag = self.repo.create_tag(
            self.next_version, message=f"{label}: {self.next_version}"
        )
        print(f"Created tag: {tag.name}")
        return tag

    def commit_version_changelog(self):
        """Commit the version and changelog files."""

        if self.repo.is_dirty():
            self.repo.index.add([self.changelog_filename, self.version_filename])
            self.repo.index.commit(
                f"Update changelog and sets version to {self.next_version}"
            )
            print("Committed Version and Changelog\n")

    def check_pre_push_hook(self):
        """Check if there is a legacy pre-push hook and delete it."""
        hook_detection_line = "skulk.run_pre_push_checks()"
        delete_hook = False
        if os.path.exists(self.hook_filename):
            with open(self.hook_filename, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() == hook_detection_line:
                        delete_hook = True
        if delete_hook:
            print(f"Found legacy pre-push hook '{self.hook_filename}' - Deleting ...")
            try:
                os.unlink(self.hook_filename)
            except IOError as ex:
                print(f"Error deleting '{self.hook_filename}': {ex}")
                util.enter_to_continue_or_exit(
                    "Please delete it manually, then press enter"
                )


def main():
    """Run the wizard."""
    wizard = Skulk()
    wizard.run()


if __name__ == "__main__":
    main()
