/*
*  @(#)Create{{ className }}ControllerTest.java
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
package {{ package }}.controllers.commands;

import {{ package }}.aggregate.{{ className }}Aggregate;
import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.protocols.{{ className }}Request;
import {{ package }}.utils.GenId;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Optional;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

/**
* class Create{{ className }}ControllerTest
*
* @author {{ username }}
**/
@WebMvcTest(Create{{ className }}Controller.class)
@DisplayName("test for create controller.")
public class Create{{ className }}ControllerTest {

    private static final String ID = GenId.newId();

    @MockBean
    private {{ className }}Aggregate aggregate;

    @Autowired
    private ObjectMapper mapper;

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
    @DisplayName("should create an entity")
    void shouldCreateEntity() throws Exception {
        when(aggregate.create(any())).thenReturn(Optional.of(entity));
        mock.perform(post("/v1/{{ project }}s")
                        .content(mapper.writeValueAsString(request))
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isCreated())
                .andDo(print())
                .andExpect(jsonPath("$.id").value(request.getId()))
        ;
    }

    @Test
    @DisplayName("should return not found")
    void shouldReturnNotFound() throws Exception {
        when(aggregate.create(any())).thenReturn(Optional.empty());

        mock.perform(post("/v1/{{ project }}s")
                        .content(mapper.writeValueAsString(request))
                        .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isNotFound())
                .andDo(print());
    }

}