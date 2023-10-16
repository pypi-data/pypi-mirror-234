/*
 *  @(#)HttpUtils.java
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
package {{ package }}.utils;

import {{ package }}.protocols.{{ className }}Response;
import lombok.experimental.UtilityClass;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

/**
* class HttpUtils
* 
* @author {{ username  }}
*/
@UtilityClass
public class HttpUtils {
    public static ResponseEntity<{{ className }}Response> CREATED ({{ className }}Response response) {
        return new ResponseEntity<>(response, HttpStatus.CREATED);
    }
}

