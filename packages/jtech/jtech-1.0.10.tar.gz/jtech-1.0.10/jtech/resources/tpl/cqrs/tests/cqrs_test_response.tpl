/*
*  @(#){{ className }}ResponseTest.java
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
package {{ package }}.protocols;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.utils.GenId;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

{%if isJpa or not isMongo %}import java.util.UUID;{% endif %}

import static com.google.code.beanmatchers.BeanMatchers.*;
import static org.hamcrest.CoreMatchers.allOf;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
* class {{ className }}ResponseTest
*
* @author {{ username }}
**/
@DisplayName("test for response class.")
class {{ className }}ResponseTest {

    @Test
    @DisplayName("should all fields is ok")
    void shouldAllFieldsIsOk() {
        assertNotNull({{ className }}Response.builder().build());
        assertThat({{ className }}Response.class,
                allOf(hasValidBeanConstructor(),
                        hasValidBeanEquals(),
                        hasValidGettersAndSetters(),
                        hasValidBeanHashCode(),
                        hasValidBeanToString()));
    }

    @Test
    @DisplayName("test instance creation")
    void testInstanceCreation() {
        var response = new {{ className }}Response();
        assertNotNull(response);
    }

    @Test
    @DisplayName("test all arguments")
    void testAllArgsConstructor() {
        var id = GenId.newId();
        var response = new {{ className }}Response(id, null);
        assertEquals(id, response.getId());
    }

    @Test
    @DisplayName("test builder class")
    void testBuilder() {
        var id = GenId.newId();
        var response = {{ className }}Response.builder()
                .id(id)
                .build();
        assertEquals(id, response.getId());
    }

    @Test
    @DisplayName("test static of method")
    void testOf() {
        var entity = new {{ className }}Entity();
        entity.setId({% if isMongo and not isJpa %}GenId.newId(){% else %}UUID.randomUUID(){% endif %});
        var response = {{ className }}Response.of(entity);
        assertNotNull(response);
        assertEquals(entity.getId().toString(), response.getId());
    }

    @Test
    @DisplayName("test json annotations present")
    void testJsonAnnotations() {
        Class<{{ className }}Response> responseClass = {{ className }}Response.class;
        assertNotNull(responseClass.getAnnotation(JsonInclude.class));
        assertNotNull(responseClass.getAnnotation(JsonIgnoreProperties.class));
    }

}