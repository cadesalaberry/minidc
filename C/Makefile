PROG=minidc
CC=gcc
CC_FLAGS=-g -O2 -c -Wall
OBJECTS=$(PROG).o

all:$(OBJECTS)
	$(CC) $(PROG).o -o $(PROG)

$(OBJECTS):%.o:%.c
	$(CC) $(CC_FLAGS) $< -o $@

clean:
	rm *.o
	rm -rf $(PROG)

