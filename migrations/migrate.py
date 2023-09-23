import os
import importlib.util
import traceback
import semver
import argparse


def run_migrations(from_version, to_version):
    migration_dir = os.path.dirname(os.path.abspath(__file__))
    migrations = []

    # Step 1: Scan the directory for migration files
    for filename in os.listdir(migration_dir):
        if filename.endswith(".py") and filename != __file__:
            module_name = filename[:-3]  # Remove .py extension
            module_path = os.path.join(migration_dir, filename)

            # Step 2: Parse the migration file
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec is None:
                print(f"Error getting spec for {filename}, skipping")
                continue
            module = importlib.util.module_from_spec(spec)
            if spec.loader is None:
                print(f"Error getting loader for {filename}, skipping")
                continue
            spec.loader.exec_module(module)

            if hasattr(module, "version") and hasattr(module, "migrate"):
                migration_version = module.version

                # Check if the migration version is within the specified range
                if (
                    semver.compare(from_version, migration_version)
                    < 0
                    <= semver.compare(to_version, migration_version)
                ):
                    migrations.append((migration_version, module.migrate))

    # Step 3: Sort migrations by version
    migrations.sort(key=lambda x: semver.VersionInfo.parse(x[0]))

    # Step 4: Execute the relevant migrations
    for version, migrate_func in migrations:
        try:
            print(f"Running migration {version}...")
            migrate_func()
            print(f"Migration {version} completed successfully.")
        except Exception as e:
            print(f"Error running migration {version}: {str(e)}")
            traceback.print_exc()

    print("Successfully ran migrations")


def main():
    parser = argparse.ArgumentParser(
        description="Run migrations between two SemVer versions."
    )
    parser.add_argument("from_version", type=str, help="The starting SemVer version")
    parser.add_argument("to_version", type=str, help="The ending SemVer version")
    args = parser.parse_args()

    run_migrations(args.from_version, args.to_version)


if __name__ == "__main__":
    main()
