/*
*  @(#){{ className }}EntityTest.java
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
package {{ package }}.entities;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static com.google.code.beanmatchers.BeanMatchers.*;
import static org.hamcrest.CoreMatchers.allOf;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
* class {{ className }}EntityTest
*
* @author {{ username }}
**/
@DisplayName("test for entity class.")
class {{ className }}EntityTest {

    @Test
    @DisplayName("should instance creation")
    void shouldInstanceCreation() {
        {{ className }}Entity entity = new {{ className }}Entity();
        assertNotNull(entity);
    }

    @Test
    @DisplayName("should all argument constructor created")
    void shouldAllArgsConstructor() {
        String id = UUID.randomUUID().toString();
        {{ className }}Entity entity = new {{ className }}Entity(id /*, other parameters*/);
        assertEquals(id, entity.getId());
    }

    @Test
    @DisplayName("should getter and setters ok")
    void shouldGettersAndSettersOk() {
        {{ className }}Entity entity = new {{ className }}Entity();
        String id = UUID.randomUUID().toString();
        entity.setId(id);
        assertEquals(id, entity.getId());
    }


    @Test
    @DisplayName("should all fields is ok")
    void shouldAllFieldsIsOk() {
        assertNotNull({{ className }}Entity.builder().build());
        assertThat({{ className }}Entity.class,
                allOf(hasValidBeanConstructor(),
                        hasValidBeanEquals(),
                        hasValidGettersAndSetters(),
                        hasValidBeanHashCode(),
                        hasValidBeanToString()));
    }


}