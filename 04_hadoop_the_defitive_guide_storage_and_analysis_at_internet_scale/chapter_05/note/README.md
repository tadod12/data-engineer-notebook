# Chapter 5. Hadoop I/O

## Data Integrity

The usual way of detecting corrupted data is by computing a `checksum` for the data when it first enters the system, and
again whenever it is transmitted across a channel that is unreliable and hence capable of corrupting the data. (checksum
just for error detection)

A commonly used error-detecting code is CRC-32. CRC-32 is used for checksumming in Hadoop’s `ChecksumFileSystem`, while
HDFS uses a more efficient variant called CRC-32C.

### Data Integrity in HDFS

HDFS transparently checksums all data written to it and by default verifies checksums when reading data.

Datanodes are responsible for verifying the data they receive before storing the data and its checksum. This applies to
data that they receive from clients and from other datanodes during replication. A client writing data sends it to a
pipeline of datanodes (as explained in **Chapter 3**), and the last datanode in the pipeline verifies the checksum. If
the datanode detects an error, the client receives a subclass of `IOException`.

When clients read data from datanodes, they verify checksums as well, comparing them with the ones stored at the
datanodes. Each datanode keeps a persistent log of checksum verifications, so it knows the last time each of its blocks
was verified. When a client successfully verifies a block, it tells the datanode, which updates its log.

> In addition to block verification on client reads, each datanode runs a DataBlockScan ner in a background thread that
> periodically verifies all the blocks stored on the datanode.

Because HDFS stores replicas of blocks, it can “heal” corrupted blocks by copying one of the good replicas to produce a
new, uncorrupted replica. The way this works is that if a client detects an error when reading a block, it reports the
bad block and the datanode it was trying to read from to the namenode before throwing a `ChecksumException`. The
namenode marks the block replica as corrupt so it doesn’t direct any more clients to it or try to copy this replica to
another datanode. It then schedules a copy of the block to be replicated on another datanode, so its replication factor
is back at the expected level. Once this has happened, the corrupt replica is deleted.

It is possible to disable verification of checksums by passing `false` to the setVerify `Checksum()` method on
`FileSystem` before using the `open()` method to read a file. The same effect is possible from the shell by using the
`-ignoreCrc` option with the `-get` or the equivalent `-copyToLocal` command.

> This feature is useful if you have a corrupt file that you want to inspect so you can decide what to do with it.

### LocalFileSystem

The Hadoop `LocalFileSystem` performs client-side checksumming. When you write a file called _filename_, the filesystem
client transparently creates a hidden file, _filename.crc_, in the same directory containing the checksums for each
chunk of the file. Checksums are verified when the file is read, and if an error is detected, `LocalFileSystem` throws
a `ChecksumException`.

Disable checksum

    Configuration conf = ...
    FileSystem fs = new RawLocalFileSystem();
    fs.initialize(null, conf);

### ChecksumFileSystem

`LocalFileSystem` uses `ChecksumFileSystem` to do its work, and this class makes it easy to add checksumming to other (
nonchecksummed) filesystems, as `ChecksumFileSystem` is just a wrapper around `FileSystem`.

    FileSystem rawFs = ...
    FileSystem checksummedFs = new ChecksumFileSystem(rawFs);

## Compression

File compression benefits:

- Reduce the space needed to store files
- Speed up data transfer across the network or to or from disk

A summary of compression formats

![compression format.png](compression%20format.png)

> The gzip is normally used, gzip file format is DEFLATE with extra headers and a footer

All compression algorithms exhibit a space/time trade-off: faster compression and decompression speeds usually come at
the expense of smaller space savings.

Create a compressed file _file.gz_ using the fastest compression method:

    gzip -1 file

> -1 mean optimize for speed, and -9 means optimize for space

The “Splittable” column indicates whether the compression format supports splitting (that is, whether you can seek to
any point in the stream and start reading from some point further on). Splittable compression formats are especially
suitable for MapReduce.

### Codecs

A _codec_ is the implementation of a compression-decompression algorithm. In Hadoop, a codec is represented by an
implementation of the `CompressionCodec` interface.

![hadoop compression codec.png](hadoop%20compression%20codec.png)

#### Compressing and decompressing streams with CompressionCodec

`CompressionCodec` has two methods that allow you to easily compress or decompress data.

To compress data being written to an output stream, use the `createOutputStream` (`OutputStream out`) method to create a
`CompressionOutputStream` to which you write your uncompressed data to have it written in compressed form to the
underlying stream.

Conversely, to decompress data being read from an input stream, call `createInputStream`(`InputStream in`) to obtain a
`CompressionInputStream`, which allows you to read uncompressed data from the underlying stream

    public class StreamCompressor {
        
        public static void main(String[] args) throws Exception {
            // 1 argument: codecClassname, such as org.apache.hadoop.io.compress.GzipCodec  
            // choose compression format
            String codecClassname = args[0];
            Class<?> codecClass = Class.forName(CodecClassname);
            
            // configuration
            Configuration conf = new Configuration();

            // create codec instance for calling method
            CompressionCodec codec = (CompressionCodec) ReflectionUtils.newInstance(codecClass, conf);
            
            // create stream to write uncompressed data
            CompressionOutputStream out = codec.createOutputStream(System.out)
            IOUtils.copyBytes(System.in, out, 4096, false);
            out.finish();
        }
    }

We use `ReflectionUtils` to construct a new instance of the codec, then obtain a compression wrapper around
`System.out`. Then we call the utility method `copyBytes()` on `IOUtils` to copy the input to the output, which is
compressed by the `CompressionOutputStream`. Finally, we call `finish()` on `CompressionOutputStream`, which tells the
compressor to finish writing to the compressed stream, but doesn’t close the stream.

#### Inferring CompressionCodecs using CompressionCodecFactory

`CompressionCodecFactory` provides a way of mapping a filename extension to a `CompressionCodec` using its `getCodec()`
method, which takes a `Path` object for the file in question.

See FileDecompressor.java

#### Native libraries

For performance, it is preferable to use a native library for compression and decompression. The Apache Hadoop binary
tarball comes with prebuilt native compression binaries for 64-bit Linux, called `libhadoop.so`. For other platforms,
you will need to compile the libraries yourself, following the BUILDING.txt instructions at the top level of the source
tree.

**CodecPool**. If you are using a native library, and you are doing a lot of compression or decompression in your
application, consider using CodecPool, which allows you to reuse compressors and decompressors, thereby amortizing the
cost of creating these objects.

### Compression and Input Splits

The gzip format uses DEFLATE to store the compressed data, and DEFLATE stores data as a series of compressed blocks. The
problem is that the start of each block is not distinguished in any way that would allow a reader positioned at an
arbitrary point in the stream to advance to the beginning of the next block, thereby synchronizing itself with the
stream. For this reason, gzip does not support splitting.

A bzip2 file, on the other hand, does provide a synchronization marker between blocks (a 48-bit approximation of pi), so
it does support splitting.

Hadoop applications process large datasets, so you should strive to take advantage of compression. Compression Format
suggestions (arranged roughly in order of most to least effective):

- Container file format such as sequence files, Avro datafiles, ORCFiles, or Parquet files, all of which support both
  compression and splitting.
- Compression format that supports splitting, such as bzip2, or one that can be indexed to support splitting, such as
  LZO.
- Split file into chunks in the application, and compress each chunk separately using any supported compression format.
- Store the files uncompressed.

### Using compression in MapReduce

If your input files are compressed, they will be decompressed automatically as they are read by MapReduce, using the
filename extension to determine which codec to use.

![compression properties.png](compression%20properties.png)

## Serialization

_Serialization_ is the process of turning structured objects into a byte stream for transmission over a network or for
writing to persistent storage. _Deserialization_ is the reverse process of turning a byte stream back into a series of
structured objects.

Serialization is used in two quite distinct areas of distributed data processing:

- Interprocess communication between nodes in Hadoop system (using RPCs): RPC protocol uses serialization to render the
  message into a binary stream to be sent to the remote node, which then deserializes the binary stream into the
  original message.
- For persistent storage

the four desirable properties of an RPC’s serialization format: (also crucial for a persistent storage format)

- Compact: Best for network bandwidth
- Fast: The serialization and deserialization process
- Extensible: Protocols change over time to meet new requirements, so it should be straightforward to evolve the
  protocol in a controlled manner for clients and servers
- Interoperable: Be able to support clients that are written in different languages to the server

Hadoop uses its own serialization format, Writables, which is certainly compact and fast, but not so easy to extend or
use from languages other than Java. Avro (a serialization system that was designed to overcome some of the limitations
of Writables) is covered in Chapter 12.

### The Writable Interface

The `Writable` interface defines two methods—one for writing its state to a `DataOutput` binary stream and one for
reading its state from a `DataInput` binary stream:

    package org.apache.hadoop.io;

    import java.io.DataOutput;
    import java.io.DataInput;
    import java.io.IOException;

    public interface Writable {
      void write(DataOutput out) throws IOException;
      void readFields(DataInput in) throws IOException;
    }

Use `IntWritable`, a wrapper for a Java `int` as data

    IntWritable writable = new IntWritable();
    writable.set(163);
    // or
    // IntWritable writable = new IntWritable(163);

To examine the serialized form of the IntWritable, we write a small helper method that wraps a
`java.io.ByteArrayOutputStream` in a `java.io.DataOutputStream` (an implementation of `java.io.DataOutput`) to capture
the bytes in the serialized stream:

    public static byte[] serialize(Writable writable) throws IOException {
      ByteArrayOutputStream out = new ByteArrayOutputStream();
      DataOutputStream dataOut = new DataOutputStream(out);
      writable.write(dataOut);  // write() method to write to out
      dataOut.close();
      return out.toByteArray();
    }

    byte[] bytes = serialize(writable);
    assertThat(bytes.length, is(4)); // int - 4 bytes

Deserialization

    public static byte[] deserialize(Writable writable, byte[] bytes) throws IOException {
      ByteArrayInputStream in = new ByteArrayInputStream(bytes);
      DataInputStream dataIn = new DataInputStream(in);
      writable.readFields(dataIn);  // readFields() method to read data from in
      dataIn.close();
      return bytes;
    }

    IntWritable newWritable = new IntWritable();
    deserialize(newWritable, bytes);
    assertThat(newWritable.get(), is(163));

### WritableComparable and comparators

Comparison of types is crucial for MapReduce, where there is a sorting phase during which keys are compared with one
another. One optimization that Hadoop provides is the `RawComparator` extension of Java’s `Comparator`:

    RawComparator<IntWritable> comparator = WritableComparator.get(IntWritable.class);

The comparator can be used to compare two IntWritable objects:

    IntWritable w1 = new IntWritable(163);
    IntWritable w2 = new IntWritable(67);
    assertThat(comparator.compare(w1, w2), greaterThan(0));

or their serialized representations:

    byte[] b1 = serialize(w1);
    byte[] b2 = serialize(w2);
    assertThat(comparator.compare(b1, 0, b1.length, b2, 0, b2.length), greaterThan(0));

### Writable Classes

#### Writable wrappers for Java primitives

![wrapper java.png](wrapper%20java.png)

When it comes to encoding integers, there is a choice between the fixed-length formats (`IntWritable` and
`LongWritable`) and the variable-length formats (`VIntWritable` and `VLongWritable`).

Writable class hierarchy

![writable class hierarchy.png](writable%20class%20hierarchy.png)

**Text**. `Text` is a Writable for UTF-8 sequences. It can be thought of as the Writable equivalent of
`java.lang.String`

    Text t = new Text("hadoop");
    assertThat(t.getLength(), is(6));
    assertThat(t.getBytes().length, is(6));
    
    assertThat(t.charAt(2), is((int) 'd'));  // charAt(index) return an `int`
    assertThat("Out of bounds", t.charAt(100), is(-1));

Text also has a `find()` method, which is analogous to `String`’s `indexOf()`:

    assertThat("Find a substring", t.find("do"), is(2));
    assertThat("Finds first 'o'", t.find("o"), is(3));
    assertThat("Finds 'o' from position 4 or later", t.find("o", 4), is(4));
    assertThat("No match", t.find("pig"), is(-1));

**Unicode**. When we start using characters that are encoded with more than a single byte, the differences between
`Text` and `String` become clear.

![unicode character.png](unicode%20character.png)

**Iteration**. Iterating over the Unicode characters in Text is complicated by the use of byte offsets for indexing,
since you can’t just increment the index. The idiom for iteration is a little obscure (see Example 5-6): turn the `Text`
object into a `java.nio.ByteBuffer`, then repeatedly call the `bytesToCodePoint()` static method on `Text` with the
buffer. This method extracts the next code point as an int and updates the position in the buffer. The end of the string
is detected when `bytesToCodePoint()` returns `–1`.

    public class TextIterator {
      
      public static void main(String[] args) {
        Text t = new Text("\u0041\u00DF\u6771\uD801\uDC00");
        
        ByteBuffer buf = ByteBuffer.wrap(t.getBytes(), 0, t.getLength());
        int cp;
        while (buf.hasRemaining() && (cp = Text.bytesToCodePoint(buf)) != -1) {
          System.out.println(Integer.toHexString(cp));
        }
      }
    }

    // % hadoop TextIterator 41 df 6771 10400

**Mutability**. Another difference from `String` is that `Text` is mutable. You can reuse a `Text` instance by calling
one of the `set()` methods on it.

    Text t = new Text("hadoop");
    t.set("pig");

**Resorting to String**. Text doesn’t have as rich an API for manipulating strings as `java.lang.String`, so in many
cases, you need to convert the `Text` object to a `String`

    assertThat(new Text("hadoop").toString(), is("hadoop"));

**BytesWritable**: Page 146

**NullWritable**: Page 147

**ObjectWritable and GenericWritable**: Page 147

**Writable Collections**. The `org.apache.hadoop.io` includes 6 `Writable` collection types:

- `ArrayWritable`
- `ArrayPrimitiveWritable`
- `TwoDArrayWritable`
- `MapWritable`
- `SortedMapWritable`
- `EnumSetWritable`

All the elements of an `ArrayWritable` or a `TwoDArrayWritable` must be instances of the same class:

    ArrayWritable writable = new ArrayWritable(Text.class);

## File-Based Data Structures

### SequenceFile

Hadoop’s `SequenceFile` provides a persistent data structure for binary key-value pairs. To use it as a logfile format,
you would choose a key, such as timestamp represented by a `LongWritable`, and the value would be a `Writable` that
represents the quantity being logged.

**Writing a SequenceFile**

To create a `SequenceFile`, use one of its `createWriter()` static methods, which return a `SequenceFile` instance. The
keys and values stored in a `SequenceFile` do not necessarily need to be `Writables`. Any types that can be serialized
and deserialized by a `Serialization` may be used.

Once you have a `SequenceFile.Writer`, you then write key-value pairs using the `append()` method. When you’ve finished,
you call the `close()` method.

    writer = SequenceFile.createWriter(fs, conf, path, key.getClass(), value.getClass());

See SequenceFileWriteDemo.java

> The `writer.getLength()` method discovers the current position in the file

**Reading a SequenceFile**

Reading sequence files from beginning to end is a matter of creating an instance of `SequenceFile.Reader` and iterating
over records by repeatedly invoking one of the `next()` methods.

    public boolean next(Writable key, Writable Value);
    // true if a key-value pair was read and false if the end of the file has been reached

Non-Writable serialization frameworks (such as Apache Thrift)

    public Object next(Object key) throws IOException
    public Object getCurrentValue(Object val) throws IOException

If the `next()` method returns a non-null object, a key-value pair was read from the stream, and the value can be
retrieved using the `getCurrentValue()` method. Otherwise, if `next()` returns null, the end of the file has been
reached.

Seek to a given position in a sequence file:

- `seek()` method, which positions the reader at the given point in the file


    // % hadoop SequenceFileReadDemo numbers.seq
    // [359] 95 One, two, buckle my shoe
    reader.seek(359);
    assertThat(reader.next(key, value), is(true)); // not null
    assertThat(((IntWritable) key).get(), is(95));

> `reader.next(key, value);` fails with `IOException` if the position in the file is not at a record boundary

- `sync(long position)` method, positions the reader at the next sync point after the `position`. If there are no sync
  point in the file after this position, then the reader will be positioned at the end of the file. Thus, we can call
  `sync()` with any position in the stream - not necessarily a record boundary - and the reader will reestablish itself
  at the next sync point so reading can continue


    // [2021*] 59 Three, four, shut the door
    reader.sync(360);
    assertThat(reader.getPosition(), is(2021L));
    assertThat(reader.next(key, value), is(true);
    assertThat(((IntWritable) key).get(), is(59));    
    
**Sorting and Merging SequenceFile**

    % hadoop jar \
    $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    sort -r 1 \
    -inFormat org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat \
    -outFormat org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat \
    -outKey org.apache.hadoop.io.IntWritable \
    -outValue org.apache.hadoop.io.Text \
    numbers.seq sorted
    % hadoop fs -text sorted/part-r-00000 | head

**The SequenceFile format**: Page 133

**Row-oriented versus column-oriented storage**

![row versus col oriented storage.png](row%20versus%20col%20oriented%20storage.png)

The first column-oriented file format in Hadoop was Hive’s RCFile, short for Record Columnar File. It has since been 
superseded by Hive’s ORCFile (Optimized Record Columnar File), and Parquet (covered in Chapter 13). Parquet is a 
general-purpose columnoriented file format based on Google’s Dremel, and has wide support across Hadoop components. 
Avro also has a column-oriented format called _Trevni_