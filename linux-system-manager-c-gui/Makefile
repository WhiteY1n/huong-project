CC=gcc
CFLAGS=-Wall -Wextra -std=c11
TARGET=bin/linux_manager
SRC=src/linux_manager.c

all:
	mkdir -p bin logs runtime test reports
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

run-gui:
	python3 app.py

.PHONY: all clean run-gui
