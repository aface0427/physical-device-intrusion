package com.xjtu.backweb.entity;

import jakarta.persistence.*;

import java.util.Date;
@Entity
@Table(name = "meter_data")
public class MeterData {
    //仅单相
    @Column(name="id")
    private Integer id;//电表编号
    @Column(name="meter_model")
    private String meterModel;//电表型号
    @Column(name="voltage_value")
    private Float voltageValue;//电表电压
    @Column(name="current_value")
    private Float currentValue;//电表电流
    @Column(name="power_value")
    private Float powerValue;//电表功率\
    @Id
    @Column(name="count")
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long count;
    @Column(name="time_step")
    private Date timeStep;
    @Column(name="ct1")
    private Integer ct1;
    @Column(name="ct2")
    private Integer ct2;
    @Column(name="pt1")
    private Integer pt1;
    @Column(name="pt2")
    private Integer pt2;

    public Long getCount() {
        return count;
    }

    public void setCount(Long count) {
        this.count = count;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getMeterModel() {
        return meterModel;
    }

    public void setMeterModel(String meterModel) {
        this.meterModel = meterModel;
    }

    public Float getVoltageValue() {
        return voltageValue;
    }

    public void setVoltageValue(Float voltageValue) {
        this.voltageValue = voltageValue;
    }

    public Float getCurrentValue() {
        return currentValue;
    }

    public void setCurrentValue(Float currentValue) {
        this.currentValue = currentValue;
    }

    public Float getPowerValue() {
        return powerValue;
    }

    public void setPowerValue(Float powerValue) {
        this.powerValue = powerValue;
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

    public Date getTimeStep() {
        return timeStep;
    }

    public void setTimeStep(Date timeStep) {
        this.timeStep = timeStep;
    }
}
