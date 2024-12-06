package book.chap03;

import org.apache.hadoop.fs.FsUrlStreamHandlerFactory;
import org.apache.hadoop.io.IOUtils;

import java.io.InputStream;
import java.net.URL; // open a stream to read data from

public class URLCat {

    // Making Java recognize Hadoop's hdfs URL scheme
    static {
        URL.setURLStreamHandlerFactory(new FsUrlStreamHandlerFactory()); // filesystem
    }

    public static void main(String[] args) throws Exception {
        InputStream in = null;
        try {
            in = new URL(args[0]).openStream();
            IOUtils.copyBytes(in, System.out, 4096, false);
            /*
            input stream            in
            output stream           out
            buffer size to copy     4096 byes
            close when copy done?   false
            */
        } finally {
            IOUtils.closeStream(in);
        }
    }
}
