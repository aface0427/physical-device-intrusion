package com.xjtu.backweb.dao;

import com.xjtu.backweb.entity.MeterData;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.transaction.Transactional;
import org.springframework.stereotype.Repository;

@Repository
@Transactional
public class MeterDataDao {
    @PersistenceContext
    private EntityManager entityManager;

    public void saveMeterData(MeterData meterData) {
        entityManager.persist(meterData);
    }
}
