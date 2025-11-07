# Build a tiny remote system:

# Receivers

# Light with on() / off()

# Fan with speeds: 0(off), 1(low), 2(medium), 3(high) and set_speed(n)

# Command interface

# execute()

# undo()

# Concrete commands

# LightOnCommand, LightOffCommand

# FanSetSpeedCommand (sets a target speed; undo() restores previous speed)

# Invoker

# Remote with press(cmd) to run a command and push it to a history stack

# undo() pops last command and calls its undo()