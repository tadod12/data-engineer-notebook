package book.chap03;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IOUtils;
import org.apache.hadoop.util.Progressable;

import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.URI;

public class FileCopyWithProgress {
    public static void main(String[] args) throws Exception {
        String localSrc = args[0];
        String dst = args[1];

        InputStream in = new BufferedInputStream(new FileInputStream(localSrc));
        // 'InputStream' can be constructed using 'Files.newInputStream()'

        Configuration conf = new Configuration();
        FileSystem fs = FileSystem.get(URI.create(dst), conf);
        OutputStream out = fs.create(new Path(dst), new Progressable() {
            public void progress() {
                System.out.println(".");
            }
        }); // anonymous new Processable() can be replace with lambda

        IOUtils.copyBytes(in, out, 4096, false);
    }
}

// mvn package
// hadoop jar .\target\hadoop_filecopywithprocess-1.0-SNAPSHOT.jar FileCopyWithProgress D:\repo_books\hadoop_filecopywithprocess\input\copy_progress.txt hdfs://localhost:9000/hadoop_guide/chap3/copy_progress.txt