/*
*  @(#)Find{{ className }}ByIdControllerTest.java
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
package {{ package }}.controllers.queries;

import {{ package }}.aggregate.{{ className }}Aggregate;
import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.protocols.{{ className }}Request;
import {{ package }}.utils.GenId;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;


import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
* class Find{{ className }}ByIdControllerTest
*
* @author {{ username }}
**/
@WebMvcTest(Find{{ className }}ByIdController.class)
@DisplayName("test for find by id controller.")
class Find{{ className }}ByIdControllerTest {

    private static final String ID = GenId.newId();

    @MockBean
    private {{ className }}Aggregate aggregate;


    private {{ className }}Entity entity = new {{ className }}Entity();

    private {{ className }}Request request = new {{ className }}Request();

    @Autowired
    private MockMvc mock;

    @BeforeEach
    void before() {
        entity.setId(ID);
        request.setId(ID);
    }

    @Test
    @DisplayName("should display an entity")
    void shouldReturnEntity() throws Exception {
        when(aggregate.findById(any())).thenReturn(entity);
        mock.perform(get("/v1/{{ project }}s/" + ID)
                        .contentType(MediaType.APPLICATION_JSON)
                ).andDo(print())
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(ID))
        ;
    }

    @Test
    @DisplayName("should return not found when entity is null")
    void shouldReturnNotFoundWhenNull() throws Exception {
        when(aggregate.findById(any())).thenReturn(null);
        mock.perform(get("/v1/{{ project }}s/" + ID)
                        .contentType(MediaType.APPLICATION_JSON)
                ).andDo(print())
                .andExpect(status().isNotFound());
    }


}