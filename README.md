# Kafka-lite Proof of Concept

### This is a concept implementation of a Kafka-like message que (known as an event queue).

Unlike real Kafka message queue, this code is intended for a single-host usage.

The idea behind is to exploit Linux (POSIX) guaranties of a file append:
* multiple append operations perform atomic writes (there is a minimum guarantied limit of 32KB);
* multiple append operations always write data in the end of the file no matter where file position was at;

The message log is a set of files with a common part in its name (topic name) and a sequence number of the chunk.

The log file is split to chunks to provide some retention policy (not implemented in the PoC).
Whenever current chunk hits preconfigured number of messages / size a new chunk is created.
The oldest chunk is cleaned up (if necessary).

The messages are stored in JSON format, but it may vary.

Successful write is the confirmation of message delivery.
fsync may be used for the guarantied write in case of system-crash,
but it is still not a 100% guaranty against of hardware faults.

Consumers read the log file (polling like in the PoC or using
select/poll/epoll/inotify/fanotify). Every message can be read by infinite
number of consumers or may be read over and over by a consumer. The consumer is
responsible for selecting the message it wants to begin reading from.
It should store the id of the last read message in a persistent storage
and seek to it after restart.
Though there is a simple solution of storing it in a separate topic
(ack(msg_id) in the PoC)
so that no other persistent storage is needed and the messages are
read only once by every consumer.

### Usage example
produce.py - produces 100k messages
process.py - reads all the messages. Has no acknowledgment - messages
are read every run over and over.
process_new.py - reads messages with acknowledgement. Consumer id may be
passed via command line parameter.

```
python produce.py                                                                                                                                    Вт 06 сен 2022 16:34:12
Last record id = 0
it took 1115 ms
```
100k messages written in 1.115 seconds.
```
python process.py                                                                                                                           1169ms  Вт 06 сен 2022 16:34:21
it took 443 ms, latency=107219083930 ns
```
100k messages read in 443 milliseconds.
```
python read_new.py
...
```
It reads 100k messages and holds for the new until Ctrl-C.
if you run it again it doesn't read old messages (unlike process.py).
Now if you delete the queue and run process and produce in parallel:
```
rm test.000*
python process.py & python produce.py                                                                                                                Вт 06 сен 2022 16:39:34
Last record id = 0
it took 1234 ms
it took 1232 ms, latency=23018 ns
```
You may see that latency of reading of the latest message was ~23 microseconds.


You may play around running process.py, process_new.py <id> and produce.py in parallel in various combinations.
