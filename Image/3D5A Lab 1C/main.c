/*
Student Name: Breandan Kerin
Student Number: 14310166
Data Structures & Algorithms Lab 1B
*/

#include<math.h>
#include<stdlib.h> // for malloc/calloc
#include<stdio.h> // for i/o
#include<string.h>

typedef unsigned char byte;

int main()
{

    int sz = 256*256*3;
    //creating a pointer called image_data that is being given memory in heap by calloc. the size of memroy is width*height*3 - for pixels, and each pixel is the size of an unsigned char??
    byte* image_data = (byte*)malloc(sz);
    memset(image_data,255, sz);

    {//printing

    for(int row = 0; row < 256; row++)
        {
            for(int col = 0; col < 256; col++)
            {
                int pxlN = row*256 + col;

                if(abs(sqrt(pow(128- row, 2) + pow(128 - col, 2))) <= 128)
                {
                    image_data[pxlN*3] = 0;
                    image_data[pxlN*3+1] = 255;
                    image_data[pxlN*3+2] = 0;
                }


                if (col == row)
                {
                    image_data[pxlN*3] = 255;
                    image_data[pxlN*3+1] = 0;
                    image_data[pxlN*3+2] = 0;
                }

/*
                if(col>170)
                {
                    image_data[pxlN*3] = 200;
                    image_data[pxlN*3+1] = 120;
                    image_data[pxlN*3+2] = 0;
                }

                if(col<85)
                {
                    image_data[pxlN*3] = 0;
                    image_data[pxlN*3+1] = 255;
                    image_data[pxlN*3+2] = 0;
                }*/
            }


        }
    }

    FILE* file_pointer = fopen("my_image1C.ppm", "w"); // (creating)opening a file called my_image, and w = write, r = read, r+w = read & write
    { //HEADER
        //fprintf prints one line to a file
        // p3 is ascii version - tells to read in ascii not binary
        fprintf(file_pointer, "P3\n256 256\n255\n");
    }
    { //BODY
        for(int y=0; y<sz;y++)
            fprintf(file_pointer, "%i ",image_data[y]);
    }
    fclose(file_pointer);

    //calls function to print out image
    //write_ppm(image_data, w, h);

    free(image_data);
    return 0;
}
