obj-m += matrix_kmod.o

KDIR := /lib/modules/$(shell uname -r)/build
PWD  := $(shell pwd)

all:
	$(MAKE) -C $(KDIR) M=$(PWD) modules

clean:
	$(MAKE) -C $(KDIR) M=$(PWD) clean

load:
	sudo insmod matrix_kmod.ko

unload:
	sudo rmmod matrix_kmod

reload: unload load

test:
	cat /proc/matrix_module

log:
	sudo dmesg | tail -n 40

install:
	sudo mkdir -p /lib/modules/$(shell uname -r)/extra
	sudo cp matrix_kmod.ko /lib/modules/$(shell uname -r)/extra/
	sudo depmod

remove-installed:
	sudo rm -f /lib/modules/$(shell uname -r)/extra/matrix_kmod.ko
	sudo depmod

.PHONY: all clean load unload reload test log install remove-installed
