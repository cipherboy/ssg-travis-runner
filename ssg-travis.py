#!/usr/bin/python3

import yaml
import subprocess


def extract_env(instance):
    env_part = instance['env'].split("=")
    env_var = env_part[0]
    env_value = env_part[1][1:-1]
    return {env_var: env_value}


def main():
    config = yaml.load(open(".travis.yml", 'r'))
    instances = config['matrix']['include']
    for instance in instances:
        env = extract_env(instance)
        for command in instance['before_install']:
            cmd = subprocess.Popen(command, shell=True, env=env)
            cmd.wait()
            if cmd.returncode != 0:
                print("Command failed %d: %s" % (cmd.returncode, cmd))
                return
        for command in instance['script']:
            cmd = subprocess.Popen(command, shell=True, env=env)
            cmd.wait()
            if cmd.returncode != 0:
                print("Command failed %d: %s" % (cmd.returncode, cmd))
                return


if __name__ == "__main__":
    main()
