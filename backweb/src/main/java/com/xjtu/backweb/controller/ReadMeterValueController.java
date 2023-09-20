package com.xjtu.backweb.controller;

import com.xjtu.backweb.common.HttpResult;
import com.xjtu.backweb.dao.MeterDataDao;
import com.xjtu.backweb.entity.MeterData;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
@Controller
@RequestMapping("/api/backweb")
@EnableScheduling
public class ReadMeterValueController {
    @Autowired
    MeterDataDao meterDataDao;
    private Socket socket;
    private Boolean isConnected=false;
    private Integer now_point=1;
    private Integer maxi=7;
    @RequestMapping(value="connectBuild.do",method= RequestMethod.GET)
    @ResponseBody
    public HttpResult buildConnection(String ipAddr,Integer port) throws IOException {
        try{
            socket = new Socket(ipAddr, port);
            isConnected=true;
            return HttpResult.SUCCESS();
        }catch(IOException e)
        {
            isConnected=false;
            e.printStackTrace();
        }

        return HttpResult.FAILURE();
    }
    @RequestMapping(value="testButton.do",method= RequestMethod.GET)
    @ResponseBody
    public HttpResult testButton(String ipAddr,Integer port){
        return HttpResult.SUCCESS();
    }
    @RequestMapping(value="connectClose.do",method= RequestMethod.GET)
    @ResponseBody
    public HttpResult closeConnection() throws IOException {
        try{
            if(isConnected)
            {
                socket.close();
                isConnected=false;
                return HttpResult.SUCCESS();
            }
            else
            {
                isConnected=false;
                return HttpResult.FAILURE_MSG("连接未建立");
            }
        }catch(IOException e)
        {
            e.printStackTrace();
        }
        return HttpResult.FAILURE();
    }
//    @RequestMapping(value="readMeterValue.do",method= RequestMethod.GET)
//    @ResponseBody
//    public HttpResult<MeterData> readMeterData(Integer id) throws IOException {
//        MeterData meterData=new MeterData();
//        try{
//            if(isConnected)
//            {
//                OutputStream outputStream = socket.getOutputStream();
//                InputStream inputStream = socket.getInputStream();
//                byte[] request=new byte[] {0x00,0x01,0x00,0x00,0x00,0x06,0x01,0x03,0x00,0x00,0x00,0x00};
//                byte[] response=new byte[512];
//                byte[] response2=new byte[512];
//                short[] res=new short[512];//byte取值-127-128，要转换一下
//                if(id==1||id==2)
//                {
//                    meterData.setId(id);
//                    meterData.setMeterModel("EPM5500P");
//                    request[6]=(byte)(id&0xFF);
//                    request[8]=0x01;
//                    request[9]=0x05;
//                    request[10]=0x00;
//                    request[11]=0x04;
//                    outputStream.write(request);
//                    outputStream.flush();
//                    int bytesRead = inputStream.read(response,0,17);
//                    for(int i=0;i<17;i++)
//                    {
//                        res[i]= (short) (response[i]&0xFF);
//                    }
//                    if(bytesRead==17)
//                    {
//                        //9-16
//                        //读PT CT
//                        meterData.setPt1((res[9] << 24) + (res[10] << 16) + (res[11] << 8) + res[12]);
//                        meterData.setPt2((res[13] << 8) + res[14]);
//                        meterData.setCt1((res[15] << 8) + res[16]);
//                        meterData.setCt2(5);
//                        request[8] = 0x01;
//                        request[9] = 0x31;
//                        request[10] = 0x00;
//                        request[11] = 0x16;
//                        outputStream.write(request);
//                        outputStream.flush();
//                        //读电压电流
//                        bytesRead = inputStream.read(response, 0, 53);
//                        for(int i=0;i<53;i++)
//                        {
//                            res[i]= (short) (response[i]&0xFF);
//                        }
//                        System.out.println(id);
//                        System.out.println(bytesRead);
//                        if (bytesRead == 53)
//                        {
//                            meterData.setVoltageValue((float) ((res[9] << 8) + res[10]) * meterData.getPt1() / meterData.getPt2() / 10.0f);
//                            meterData.setCurrentValue((float) ((res[25] << 8) + res[26]) * meterData.getCt1() / meterData.getCt2() / 1000.0f);
//                            meterData.setPowerValue((float) ((res[51] << 8) + res[52]) * meterData.getPt1() / meterData.getPt2() * meterData.getCt1() / meterData.getCt2());
//                        }
//                    }
//                }
//                else if(id==3||id==4)
//                {
//                    meterData.setId(id);
//                    meterData.setMeterModel("PM800");
//                    request[6]=(byte)(id&0xFF);
//                    request[8]=0x2d;
//                    request[9]= (byte)(0xb3&0xFF);
//                    request[10]=0x00;
//                    request[11]=0x38;
//                    outputStream.write(request);
//                    outputStream.flush();
//                    int bytesRead = inputStream.read(response,0,121);
//                    for(int i=0;i<121;i++)
//                    {
//                        res[i]= (short) (response[i]&0xFF);
//                    }
//                    if(bytesRead==121)
//                    {
//                        meterData.setVoltageValue(getFloat(response,49));
//                        meterData.setCurrentValue(getFloat(response,9));
//                        float bb=getFloat(response,117);
//                        float value = 1.0f;
//                        float epsilon = 0.000001f;
//                        meterData.setPowerValue((bb >= 1.0f - epsilon && bb <= 1.0f + epsilon)?  0.0f :getFloat(response,117)*100.0f);
//                    }
//                }
//                else if(id==5||id==6)
//                {
//                    request[6]=(byte)(id&0xFF);
//                    request[8]=0x00;
//                    request[9]=0x01;
//                    request[10]=0x00;
//                    request[11]=0x40;
//                    meterData.setId(id);
//                    meterData.setMeterModel("PAC4200");
//                    outputStream.write(request);
//                    outputStream.flush();
//                    int bytesRead = inputStream.read(response,0,137);
//                    if(bytesRead==137)
//                    {
//                        meterData.setVoltageValue(getFloat(response,9));
//                        meterData.setCurrentValue(getFloat(response,33));
//                        meterData.setPowerValue(getFloat(response,133));
//                    }
//                }
//                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
//                try {
//                    Date currentDate = new Date(); // 获取当前时间
//                    String dateString = dateFormat.format(currentDate); // 将当前时间格式化为字符串
//                    Date date = dateFormat.parse(dateString); // 将字符串解析为Date对象
//                    meterData.setTimeStep(date);
//                } catch (ParseException e) {
//                    e.printStackTrace();
//                }
//                meterDataDao.saveMeterData(meterData);
//                return HttpResult.SUCCESS(meterData);
//            }
//            else
//            {
//                isConnected=false;
//                return HttpResult.FAILURE_MSG("连接未建立");
//            }
//        }catch(IOException e)
//        {
//            e.printStackTrace();
//        }
//        return HttpResult.FAILURE();
//    }
    @Scheduled(fixedRate = 1000)
    public void readMeterDataByTicks() throws IOException {
        MeterData meterData=new MeterData();
        try{
            if(isConnected)
            {
                OutputStream outputStream = socket.getOutputStream();
                InputStream inputStream = socket.getInputStream();
                byte[] request=new byte[] {0x00,0x01,0x00,0x00,0x00,0x06,0x01,0x03,0x00,0x00,0x00,0x00};
                byte[] response=new byte[512];
                byte[] response2=new byte[512];
                short[] res=new short[512];//byte取值-127-128，要转换一下
                if(now_point==1||now_point==2)
                {
                    meterData.setId(now_point);
                    meterData.setMeterModel("EPM5500P");
                    request[6]=(byte)(now_point&0xFF);
                    request[8]=0x01;
                    request[9]=0x05;
                    request[10]=0x00;
                    request[11]=0x04;
                    outputStream.write(request);
                    outputStream.flush();
                    int bytesRead = inputStream.read(response,0,17);
                    for(int i=0;i<17;i++)
                    {
                        res[i]= (short) (response[i]&0xFF);
                    }
                    if(bytesRead==17)
                    {
                        //9-16
                        //读PT CT
                        meterData.setPt1((res[9] << 24) + (res[10] << 16) + (res[11] << 8) + res[12]);
                        meterData.setPt2((res[13] << 8) + res[14]);
                        meterData.setCt1((res[15] << 8) + res[16]);
                        meterData.setCt2(5);
                        request[8] = 0x01;
                        request[9] = 0x31;
                        request[10] = 0x00;
                        request[11] = 0x16;
                        outputStream.write(request);
                        outputStream.flush();
                        //读电压电流
                        bytesRead = inputStream.read(response, 0, 53);
                        for(int i=0;i<53;i++)
                        {
                            res[i]= (short) (response[i]&0xFF);
                        }
                        if (bytesRead == 53)
                        {
                            meterData.setVoltageValue((float) ((res[9] << 8) + res[10]) * meterData.getPt1() / meterData.getPt2() / 10.0f);
                            meterData.setCurrentValue((float) ((res[25] << 8) + res[26]) * meterData.getCt1() / meterData.getCt2() / 1000.0f);
                            meterData.setPowerValue((float) ((res[51] << 8) + res[52]) * meterData.getPt1() / meterData.getPt2() * meterData.getCt1() / meterData.getCt2());
                        }
                    }
                }
                else if(now_point==3||now_point==4)
                {
                    meterData.setId(now_point);
                    meterData.setMeterModel("PM800");
                    request[6]=(byte)(now_point&0xFF);
                    request[8]=0x2d;
                    request[9]= (byte)(0xb3&0xFF);
                    request[10]=0x00;
                    request[11]=0x38;
                    outputStream.write(request);
                    outputStream.flush();
                    int bytesRead = inputStream.read(response,0,121);
                    for(int i=0;i<121;i++)
                    {
                        res[i]= (short) (response[i]&0xFF);
                    }
                    if(bytesRead==121)
                    {
                        meterData.setVoltageValue(getFloat(response,49));
                        meterData.setCurrentValue(getFloat(response,9));
                        float bb=getFloat(response,117);
                        float value = 1.0f;
                        float epsilon = 0.000001f;
                        meterData.setPowerValue((bb >= 1.0f - epsilon && bb <= 1.0f + epsilon)?  0.0f :getFloat(response,117)*100.0f);
                    }
                }
                else if(now_point==5||now_point==6)
                {
                    request[6]=(byte)(now_point&0xFF);
                    request[8]=0x00;
                    request[9]=0x01;
                    request[10]=0x00;
                    request[11]=0x40;
                    meterData.setId(now_point);
                    meterData.setMeterModel("PAC4200");
                    outputStream.write(request);
                    outputStream.flush();
                    int bytesRead = inputStream.read(response,0,137);
                    if(bytesRead==137)
                    {
                        meterData.setVoltageValue(getFloat(response,9));
                        meterData.setCurrentValue(getFloat(response,33));
                        meterData.setPowerValue(getFloat(response,133));
                    }
                }
                SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                try {
                    Date currentDate = new Date(); // 获取当前时间
                    String dateString = dateFormat.format(currentDate); // 将当前时间格式化为字符串
                    Date date = dateFormat.parse(dateString); // 将字符串解析为Date对象
                    meterData.setTimeStep(date);
                } catch (ParseException e) {
                    e.printStackTrace();
                }
                meterDataDao.saveMeterData(meterData);
            }
            else
            {
                isConnected=false;
            }
        }catch(IOException e)
        {
            e.printStackTrace();
        }
        now_point++;
        if(now_point==maxi)now_point=1;
    }
    private static float getFloat(byte[] b,int index)
    {
        int accum=0;
        accum|=(b[0+index]&0xFF)<<24;
        accum|=(b[1+index]&0xFF)<<16;
        accum|=(b[2+index]&0xFF)<<8;
        accum|=(b[3+index]&0xFF)<<0;
        return Float.intBitsToFloat(accum);
    }
}
