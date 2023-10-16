/*
*  @(#)Create{{ className }}ServiceImplTest.java
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
package {{ package }}.services.commands.impl;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.repositories.{{ className }}Repository;
import {{ package }}.services.commands.command.Create{{ className }}Command;
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import java.util.UUID;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

/**
* class Create{{ className }}ServiceImplTest
*
* @author {{ username }}
**/
@ExtendWith(SpringExtension.class)
@DisplayNameGeneration(DisplayNameGenerator.ReplaceUnderscores.class)
@DisplayName("test for create service class.")
class Create{{ className }}ServiceImplTest {

    private static final String GEN_ID = UUID.randomUUID().toString();

    @InjectMocks
    private Create{{ className }}ServiceImpl create{{ className }}Service;

    @Mock
    private {{ className }}Repository repository;

    private {{ className }}Entity sample;

    @BeforeEach
    public void before() {
        sample = new {{ className }}Entity(GEN_ID);
        when(repository.save(any())).thenReturn(sample);
    }

    @Test
    @DisplayName("should create entity")
    void shouldCreateEntity() {
        var expected = create{{ className }}Service.create(Create{{ className }}Command.builder()
                .id(GEN_ID)
                .build());
        assertThat(expected.isPresent()).isTrue();
        assertThat(expected.get().getId()).isEqualTo(sample.getId());
    }

}