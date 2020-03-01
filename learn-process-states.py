#!/usr/bin/env python3

import os
import sys
import time
import click
import signal


def running_process(num_of_seconds):
    t_end = time.time() + num_of_seconds
    print(
        "My process ID is: {} and I am going to run for {} seconds.".format(
            os.getpid(),
            num_of_seconds))
    command = "ps aux | grep " + str(os.getpid())
    print("You can run this command to get more info on me: {}".format(command))
    while time.time() < t_end:
        # Doing a random operation
        a = 2 * 100


def sleeping_process(num_of_seconds):
    time.sleep(2)
    print(
        "My process ID is: {} and I am going to sleep for {} seconds.".format(
            os.getpid(),
            num_of_seconds))
    command = "ps aux | grep " + str(os.getpid())
    print("You can run this command to get more info on me: {}".format(command))
    time.sleep(num_of_seconds)


def stopped_process(num_of_processes):
    for i in range(num_of_processes):
        try:
            new_process = os.fork()
        except BlockingIOError:
            print(
                "Ohhhh my, you have exhausted all the pid for the system. Waiting for you to press ctrl+c")
            time.sleep(100)
        if new_process == 0:
            child_pid = os.getpid()
            print("{} process ID is: {}".format(i + 1, child_pid))
            command = "ps aux | grep " + str(child_pid)
            print(
                "You can run this command to get more info on me: {}".format(command))
            os.kill(child_pid, signal.SIGSTOP)
        else:
            time.sleep(2)
    print("All above processes are stopped now, sleeping for 10 seconds")
    time.sleep(10)


def zombie_process(num_of_processes):
    for i in range(num_of_processes):
        try:
            new_process = os.fork()
        except BlockingIOError:
            time.sleep(2)
            print(
                "Ohhhh my, you have exhausted all the pid for the system. Waiting for you to press ctrl+c")
            time.sleep(100)
        if new_process == 0:
            child_pid = os.getpid()
            print("{} process ID is: {}".format(i + 1, child_pid))
            command = "ps -o ppid,user,pid,stat,command -p " + str(child_pid)
            print(
                "You can run this command to get more info on me: {}".format(command))
            os._exit(0)
        else:
            time.sleep(1)
    print("All above processes are zombies now")


def orphan_process():
    new_process = os.fork()
    if new_process == 0:
        child_pid = os.getpid()
        print(
            "My process ID is: {} and I am going to be an orphan for {} seconds.".format(
                os.getpid(),
                100))
        command = "ps -o ppid,user,pid,stat,command -p " + str(child_pid)
        print("You can run this command to get more info on me: {}".format(command))
        time.sleep(100)
    else:
        sys.exit(0)


def main():
    print("Let us learn about process states!")
    parent_pid = os.getpid()
    print("The process id of this process is: {}".format(str(parent_pid)))
    while True:
        process_state = click.prompt(
            "What state of a process would you like to see? \n1.Running \n2.Sleeping \n3.Zombie\n4.Stopped\n5.Orphan\n6.Exit\nChoice",
            type=int)
        if process_state == 6:
            sys.exit(0)
        if process_state == 1:
            num_of_seconds = click.prompt(
                "How many seconds would you like to run for? ", type=int)
            running_process(num_of_seconds)
        elif process_state == 2:
            num_of_seconds = click.prompt(
                "How many seconds would you like to sleep for? ", type=int)
            sleeping_process(num_of_seconds)
        elif process_state == 3:
            num_of_processes = click.prompt(
                "How many such processes would you like to see? ", type=int)
            zombie_process(num_of_processes)
        elif process_state == 4:
            num_of_processes = click.prompt(
                "How many such processes would you like to see? ", type=int)
            stopped_process(num_of_processes)
        elif process_state == 5:
            orphan_process()
        else:
            print("Invalid input!!!")


if __name__ == "__main__":
    main()
