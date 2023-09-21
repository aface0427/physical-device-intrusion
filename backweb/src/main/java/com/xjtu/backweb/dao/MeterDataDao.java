package com.xjtu.backweb.dao;

import com.xjtu.backweb.entity.MeterData;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.TypedQuery;
import jakarta.transaction.Transactional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

@Repository
@Transactional
public class MeterDataDao {
    @PersistenceContext
    private EntityManager entityManager;

    public void saveMeterData(MeterData meterData) {
        entityManager.persist(meterData);
    }
    public MeterData findLastRecordById(Integer id) {
        String queryString = "SELECT m FROM MeterData m WHERE m.id = :id ORDER BY m.count DESC";
        TypedQuery<MeterData> query = entityManager.createQuery(queryString, MeterData.class);
        query.setParameter("id", id);
        query.setMaxResults(1);
        return query.getSingleResult();
    }
    public MeterData[] findLastSixRecordById() {
        MeterData[] ne=new MeterData[6];
        String queryString = "SELECT m FROM MeterData m WHERE m.id = :id ORDER BY m.count DESC";
        TypedQuery<MeterData> query = entityManager.createQuery(queryString, MeterData.class);
        for(int i=0;i<=5;i++)
        {
            query.setParameter("id", i+1);
            query.setMaxResults(1);
            ne[i]=query.getSingleResult();
        }
        return ne;
    }
}
