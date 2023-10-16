/*
*  @(#)Find{{ className }}ByIdQueryTest.java
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
package {{ package }}.services.queries.query;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
* class Find{{ className }}ByIdQueryTest
*
* @author {{ username }}
**/
@DisplayName("test for find by id query.")
class Find{{ className }}ByIdQueryTest {
    @Test
    @DisplayName("should all fields is ok")
    void shouldCreateSuccess() throws Exception {
        var query = new Find{{ className }}ByIdQuery(UUID.randomUUID()/*, others parameters */);
        assertNotNull(query);
    }

}