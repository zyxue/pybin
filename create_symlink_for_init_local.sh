# put configuration files you wanna version control here and make symlinks to the
# outside.

# STEPS:

# 1. move the interested files here, removing the prefixed dot
# 2. use the following command in the home directory to make symlinks
for i in .init_local/[a-z]*; do ln -s -f ${i} .$(basename ${i}) ;done
