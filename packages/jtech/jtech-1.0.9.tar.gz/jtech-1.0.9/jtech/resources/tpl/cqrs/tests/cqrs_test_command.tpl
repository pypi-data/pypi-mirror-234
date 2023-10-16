/*
*  @(#)Create{{ className }}CommandTest.java
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
package {{ package }}.services.commands.command;

import {{ package }}.utils.GenId;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static com.google.code.beanmatchers.BeanMatchers.*;
import static org.assertj.core.api.Assertions.assertThat;
import static org.hamcrest.CoreMatchers.allOf;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
* class Create{{ className }}CommandTest
*
* @author {{ username }}
**/
@DisplayName("test for create command class.")
class Create{{ className }}CommandTest {


    @Test
    @DisplayName("should create command with all data")
    void shouldCreateWithAllData() {
        var command = new Create{{ className }}Command(GenId.newId()/*, other parameters*/);
        assertThat(command).isNotNull();
    }

    @Test
    @DisplayName("should create a command and test fields")
    void shouldCreateCommandAndTestFields() {
        assertThat(new Create{{ className }}Command()).isNotNull();
        org.hamcrest.MatcherAssert.assertThat(Create{{ className }}Command.class,
                allOf(hasValidBeanConstructor(),
                        hasValidBeanEquals(),
                        hasValidGettersAndSetters(),
                        hasValidBeanHashCode(),
                        hasValidBeanToString()));
    }

    @Test
    @DisplayName("should be transformed to entity")
    void testToEntity() {
        var genId = GenId.newId();
        var command = Create{{ className }}Command.builder()
                .id(genId)
                .build();
        var entity = command.toEntity();
        assertNotNull(entity);
        assertEquals(genId, entity.getId().toString());
    }


}