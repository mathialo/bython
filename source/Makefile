CC = gcc
CFLAGS = -Wall -pedantic

%.o: %.c
	$(CC) -c $(CFLAGS) $< 


all: bython.o
	$(CC) -o ../binaries/bython bython.o
	rm *o
