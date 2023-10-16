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
import {{ package }}.utils.GenId;
import org.assertj.core.api.AssertionsForClassTypes;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mongounit.MongoUnitTest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;


@SpringBootTest
@MongoUnitTest(name = "{{ project }}Repository")
@DisplayName("Repository test")
class {{ className }}RepositoryTest {

    private static final String GEN_ID = GenId.newId();

    @Autowired
    private {{ className }}Repository repository;

    private {{ className }}Entity entity;

    @BeforeEach
    public void before() {
        entity = {{ className }}Entity.builder()
                .id(GEN_ID)
                .build();
    }

    @Test
    @DisplayName("Create entity")
    void shouldCreateEntity() {
        var expected = this.repository.save(entity);
        AssertionsForClassTypes.assertThat(expected.getId()).isEqualTo(expected.getId());
        AssertionsForClassTypes.assertThat(expected.getId()).isNotNull();
    }

    @Test
    @DisplayName("Update entity")
    void shouldUpdateEntity() {
        var saved = this.repository.save(entity);
        AssertionsForClassTypes.assertThat(saved.getId()).isEqualTo(GEN_ID);
        saved.setId(GenId.newId(GEN_ID));
        var expected = this.repository.save(saved);
        AssertionsForClassTypes.assertThat(saved.getId()).isEqualTo(expected.getId());
        AssertionsForClassTypes.assertThat(expected.getId()).isEqualTo(GEN_ID);
    }

    @Test
    @DisplayName("Find by id")
    void shouldFindById() {
        var saved = this.repository.save(entity);
        var expected = this.repository.findById(GEN_ID);
        AssertionsForClassTypes.assertThat(expected.isPresent()).isTrue();
        AssertionsForClassTypes.assertThat(expected.get().getId()).isEqualTo(saved.getId());
    }

    @Test
    @DisplayName("Find all")
    void shouldFindAll() {
        var saved = this.repository.save(entity);
        var expected = this.repository.findAll();
        assertThat(expected).asList().isNotEmpty();
        assertThat(expected).asList().contains(saved);
    }

    @Test
    @DisplayName("Delete entity")
    void shouldDeleteEntity() {
        var saved = this.repository.save(entity);
        assertThat(saved).isNotNull();
        this.repository.deleteById(saved.getId());
        var expected = this.repository.findById(saved.getId());
        assertThat(expected.isEmpty()).isTrue();
    }

}