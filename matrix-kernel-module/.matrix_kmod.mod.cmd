savedcmd_matrix_kmod.mod := printf '%s\n'   matrix_kmod.o | awk '!x[$$0]++ { print("./"$$0) }' > matrix_kmod.mod
