/*
*  @(#)Find{{ className }}ByIdServiceImplTest.java
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
package {{ package }}.services.queries.impl;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.repositories.{{ className }}Repository;
import {{ package }}.services.queries.query.Find{{ className }}ByIdQuery;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.Optional;
import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

/**
* class Find{{ className }}ByIdServiceImplTest
*
* @author {{ username }}
**/
@ExtendWith(SpringExtension.class)
@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)
@DisplayName("test for find by id class.")
class Find{{ className }}ByIdServiceImplTest {
    private static final String GEN_ID = UUID.randomUUID().toString();

    @InjectMocks
    private Find{{ className }}ByIdServiceImpl find{{ className }}ByIdService;

    @Mock
    private {{ className }}Repository repository;

    private {{ className }}Entity sample;

    @BeforeEach
    public void before() {
        sample = new {{ className }}Entity(UUID.fromString(GEN_ID));
        when(repository.findById(any())).thenReturn(Optional.of(sample));
    }

    @Test
    @DisplayName("should return an entity")
    void shouldCreateEntity() {
        var expected = find{{ className }}ByIdService.findById(new Find{{ className }}ByIdQuery(UUID.fromString(GEN_ID)));
        assertThat(expected.getId()).isEqualTo(sample.getId());
    }
}