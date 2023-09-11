using System;
using System.Collections.Generic;
using System.Text;

namespace ConvertDataType
{
    class Program
    {
        static void Main(string[] args)
        {
            ushort[] data;
            //Convert ushort array to Long, data[0]=>Low Word, data[1]=>High Word
            data = new ushort[2] { 4, 65535 };
            long longValue;
            longValue =(Int32)(((UInt32)data[1] << 16) | (UInt32)data[0]);
            Console.WriteLine(longValue.ToString()); //-65532
            Console.ReadLine();
            
            //Convert ushort array to UnsignedLong, data[0]=>Low Word, data[1]=>High Word
            data = new ushort[2] { 25520,13587 };
            ulong ulongValue;
            ulongValue = (UInt32)(((UInt32)data[1] << 16) | (UInt32)data[0]);
            Console.WriteLine(ulongValue.ToString()); //890463152
            Console.ReadLine();
            
            //Convert ushort array to Hex 
            data = new ushort[1] { 65535};          
            Console.WriteLine(data[0].ToString("X4")); //FFFF
            Console.ReadLine();
           
            //Convert ushort array to Float 
            data = new ushort[2] { 19311, 65529 };         
            float[] floatData = new float[data.Length / 2];
            Buffer.BlockCopy(data, 0, floatData, 0, data.Length * 2);
            for (int index = 0; index < floatData.Length; index += 2)
            {
                Console.WriteLine(floatData[index / 2].ToString("0.0000")); //123.4560
                Console.ReadLine();              
            }
            
            //Convert to double
            data = new ushort[4] { 65512, 59784, 64790, 16675 };
            double[] doubleData = new double[2];
            Buffer.BlockCopy(data, 0, doubleData, 0, 8);
            Console.WriteLine(doubleData[0].ToString());
            //Convert ushort value to Int16                         
            ushort ushortValue = 65516 ;
            Int16 int16Value = (Int16)ushortValue;
            Console.WriteLine(int16Value.ToString()); //-20
            Console.ReadLine();

            //------------------------------------------------------------------------------------------
            
            ushort[] uintData = new ushort[2];  
   
            //Convert Long value to ushort array                             
            long[] longData ;
            longData = new long[1] { -65532 };
            Buffer.BlockCopy(longData, 0, uintData,0 , 4);
            for (int index = 0; index < uintData.Length; index ++)
            {
                //uintData[0] = 4 ;uintData[1] = 65535
                Console.WriteLine(string.Format("uintData[{0}] = {1}", index, uintData[index]));              
            }
            Console.ReadLine();

            //Convert UnsignedLong value to ushort array          
            ulong[] ulongData;
            ulongData = new ulong[1] { 890463152 }; 
            Buffer.BlockCopy(ulongData, 0, uintData, 0, 4);
            for (int index = 0; index < uintData.Length; index++)
            {
                //uintData[0] = 25520;uintData[1] = 13587
                Console.WriteLine(string.Format("uintData[{0}] = {1}", index, uintData[index]));
            }
            Console.ReadLine();

            //Convert Hex to ushort
            string hexValue = "FFEC";     
            Console.WriteLine(Convert.ToInt32(hexValue, 16));  //65516       
            Console.ReadLine();

            //Convert Float to short 
            floatData = new float[1] { 223.4560f };
            Buffer.BlockCopy(floatData, 0, uintData, 0, 4);
            for (int index = 0; index < uintData.Length; index++)
            {
                //uintData[0] = 29884 ;uintData[1] = 17247
                Console.WriteLine(string.Format("uintData[{0}] = {1}", index, uintData[index]));
            }
            Console.ReadLine();
      
            //Convert Int16 value to ushort           
            int16Value = -35;
            ushort uintValue = (ushort)int16Value;
            Console.WriteLine(uintValue.ToString()); //65501
            Console.ReadLine();
            
        }
    }
}

