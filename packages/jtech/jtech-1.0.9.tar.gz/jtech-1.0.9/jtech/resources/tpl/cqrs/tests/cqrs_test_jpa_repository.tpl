/*
*  @(#){{ className }}RepositoryTest.java
*
*  Copyright (c) J-Tech Solucoes em Informatica.
*  All Rights Reserved.
*
*  This software is the confidential and proprietary information of J-Tech.
*  ("Confidential Information"). You shall not disclose such Confidential
*  Information and shall use it only in accordance with the terms of the
*  license agreement you entered into with J-Tech.
*
*/
package {{ package }}.repositories;

import {{ package }}.entities.{{ className }}Entity;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.test.context.ActiveProfiles;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;

/**
* class {{ className }}RepositoryTest
*
* @author {{ username }}
**/
@DataJpaTest
@ActiveProfiles("test")
@DisplayName("test for repository interface.")
class {{ className }}RepositoryTest {

    @Autowired
    private {{ className }}Repository repository;

    @Autowired
    private TestEntityManager entityManager;


    @Test
    @DisplayName("should create entity")
    void shouldCreateEntitySuccess() {
        var entity = new {{ className }}Entity(UUID.randomUUID());
        var savedEntity = repository.save(entity);
        assertNotNull(savedEntity.getId());
        Optional<{{ className }}Entity> retrievedEntity = repository.findById(savedEntity.getId());
        assertTrue(retrievedEntity.isPresent());
        assertEquals(savedEntity.getId(), retrievedEntity.get().getId());
    }

    @Test
    @DisplayName("test find all entities")
    void testFindAllEntities() {
        var entity1 = new {{ className }}Entity();
        entityManager.persist(entity1);
        var entity2 = new {{ className }}Entity();
        entityManager.persist(entity2);
        List<{{ className }}Entity> entities = repository.findAll();
        assertEquals(2, entities.size());
    }

    @Test
    @DisplayName("find entity by id")
    void testFindEntityById() {
        var entity = new {{ className }}Entity();
        entityManager.persist(entity);
        var retrievedEntity = repository.findById(entity.getId());
        assertTrue(retrievedEntity.isPresent());
        assertEquals(entity.getId(), retrievedEntity.get().getId());
    }

}