package com.xjtu.backweb.entity;

public class MeterConfig {
    private Integer id;
    private Integer voltageThreshold;
    private Integer currentThreshold;
    private Integer powerThreshold;
    private Integer pt1;
    private Integer pt2;
    private Integer ct1;
    private Integer ct2;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getVoltageThreshold() {
        return voltageThreshold;
    }

    public void setVoltageThreshold(Integer voltageThreshold) {
        this.voltageThreshold = voltageThreshold;
    }

    public Integer getCurrentThreshold() {
        return currentThreshold;
    }

    public void setCurrentThreshold(Integer currentThreshold) {
        this.currentThreshold = currentThreshold;
    }

    public Integer getPowerThreshold() {
        return powerThreshold;
    }

    public void setPowerThreshold(Integer powerThreshold) {
        this.powerThreshold = powerThreshold;
    }

    public Integer getPt1() {
        return pt1;
    }

    public void setPt1(Integer pt1) {
        this.pt1 = pt1;
    }

    public Integer getPt2() {
        return pt2;
    }

    public void setPt2(Integer pt2) {
        this.pt2 = pt2;
    }

    public Integer getCt1() {
        return ct1;
    }

    public void setCt1(Integer ct1) {
        this.ct1 = ct1;
    }

    public Integer getCt2() {
        return ct2;
    }

    public void setCt2(Integer ct2) {
        this.ct2 = ct2;
    }
}
