// From chapter 02
package book.chap02;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class MaxTemperature {
    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.out.println("Usage: MaxTemperatureWithCompression <input file> <output file>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Max temperature With Compression");

        job.setJarByClass(MaxTemperature.class);
        job.setJobName("Max temperature With Compression");

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        // set compression
        FileOutputFormat.setCompressOutput(job, true); // compress - true
        FileOutputFormat.setOutputCompressorClass(job, GzipCodec.class); // format

        job.setMapperClass(MaxTemperatureMapper.class);
        job.setCombinerClass(MaxTemperatureReducer.class);
        job.setReducerClass(MapTemperatureReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

// hadoop jar .\target\max_temperature-1.0-SNAPSHOT.jar book.chap02.MaxTemperature input output
