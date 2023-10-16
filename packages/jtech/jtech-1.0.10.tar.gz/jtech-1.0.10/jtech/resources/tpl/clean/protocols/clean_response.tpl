/*
*  @(#){{ className }}Response.java
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
package {{ package }}.adapters.input.protocols;

import {{ package }}.application.core.domains.{{ className }};
import {{ package }}.adapters.output.repositories.entities.{{ className }}Entity;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.beans.BeanUtils;

import java.io.Serializable;
import java.util.List;

/**
* class {{ className  }}Response 
* 
* user {{ username  }} 
*/
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonIgnoreProperties(ignoreUnknown = true)
public class {{ className }}Response implements Serializable {
    private String id;
    List<{{ className }}Response> responses;

    public static {{ className }}Response of({{ className }} {{ project }}) {
        return {{ className }}Response.builder()
                .id({{ project }}.getId())
                .build();
    }

    public static {{ className }}Response of(List<{{ className }}Entity> entities) {
        var list = entities.stream().map({{ className }}Response::of).toList();
        return {{ className }}Response.builder()
                .responses(list)
                .build();
    }

    public static {{ className }}Response of({{ className }}Entity entity) {
        var response = new {{ className }}Response();
        BeanUtils.copyProperties(entity, response);
        return response;
    }
}
