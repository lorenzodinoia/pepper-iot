package it.uniba.di.sysag.pepper4rsa.utils;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;

import com.aldebaran.qi.sdk.QiContext;
import com.aldebaran.qi.sdk.builder.ExplorationMapBuilder;
import com.aldebaran.qi.sdk.object.actuation.ExplorationMap;
import com.aldebaran.qi.sdk.object.actuation.MapTopGraphicalRepresentation;
import com.aldebaran.qi.sdk.object.image.EncodedImage;
import com.aldebaran.qi.sdk.object.streamablebuffer.StreamableBuffer;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.ByteBuffer;

public final class ExplorationUtils {
    public static void saveExploration(ExplorationMap explorationMap, String name, Context context) {
        StreamableBuffer buffer = explorationMap.serializeAsStreamableBuffer();
        ByteBuffer byteBuffer = buffer.read(0L, buffer.getSize());
        try {
            FileOutputStream fileOutputStream = context.openFileOutput((name + ".txt"), Context.MODE_PRIVATE);
            fileOutputStream.write(byteBuffer.array());
            fileOutputStream.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static ExplorationMap loadExploration(String name, Context context, QiContext qiContext) {
        StringBuilder text = new StringBuilder();
        try {
            FileInputStream fileInputStream = context.openFileInput((name + ".txt"));
            InputStreamReader inputStreamReader = new InputStreamReader(fileInputStream);
            BufferedReader bufferedReader = new BufferedReader(inputStreamReader);
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                text.append(line);
                text.append('\n');
            }
            bufferedReader.close();
        }
        catch (IOException e) {
            e.printStackTrace();
        }

        String mapData = text.toString();
        return ExplorationMapBuilder.with(qiContext).withMapString(mapData).build();
    }

    public static Bitmap getBitmap(ExplorationMap explorationMap) {
        MapTopGraphicalRepresentation representation = explorationMap.getTopGraphicalRepresentation();
        EncodedImage encodedImage = representation.getImage();
        byte[] imageAsByte = encodedImage.getData().array();
        return BitmapFactory.decodeByteArray(imageAsByte, 0, imageAsByte.length);
    }
}
