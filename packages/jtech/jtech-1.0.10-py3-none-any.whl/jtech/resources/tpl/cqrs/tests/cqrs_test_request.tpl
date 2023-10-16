/*
*  @(#){{ className }}RequestTest.java
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

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static com.google.code.beanmatchers.BeanMatchers.*;
import static org.hamcrest.CoreMatchers.allOf;
import static org.hamcrest.MatcherAssert.assertThat;
import static org.junit.jupiter.api.Assertions.assertNotNull;

/**
* class {{ className }}RequestTest
*
* @author {{ username }}
**/
@DisplayName("test for request class.")
class {{ className }}RequestTest {

    @Test
    @DisplayName("should all fields is ok")
    void shouldAllFieldsIsOk() {
        assertNotNull({{ className }}Request.builder().build());
        assertThat({{ className }}Request.class,
                allOf(hasValidBeanConstructor(),
                        hasValidBeanEquals(),
                        hasValidGettersAndSetters(),
                        hasValidBeanHashCode(),
                        hasValidBeanToString()));
    }
}