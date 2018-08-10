#!/usr/bin/python3

import yaml
import subprocess
import sys


def extract_env(instance):
    env_part = instance['env'].split("=")
    env_var = env_part[0]
    env_value = env_part[1][1:-1]
    return {env_var: env_value}


def run_instance(instance):
    env = extract_env(instance)
    for command in instance['before_install']:
        cmd = subprocess.Popen(command, shell=True, env=env)
        cmd.wait()
        if cmd.returncode != 0:
            print("Command failed %d: %s" % (cmd.returncode, command))
            return False

    for command in instance['script']:
        cmd = subprocess.Popen(command, shell=True, env=env)
        cmd.wait()
        if cmd.returncode != 0:
            print("Command failed %d: %s" % (cmd.returncode, command))
            return False

    return True


def main():
    config = yaml.load(open(".travis.yml", 'r'))
    instances = config['matrix']['include']

    if len(sys.argv) == 1:
        for instance in instances:
            ok = run_instance(instance)
            if not ok:
                sys.exit(1)
    else:
        for num in sys.argv[1].split(','):
            ok = run_instance(instances[int(num)])
            if not ok:
                sys.exit(1)


if __name__ == "__main__":
    main()
