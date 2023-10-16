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
package {{ package }}.protocols;

import {{ package }}.entities.{{ className }}Entity;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
import java.util.List;
{%if isJpa %}import java.util.UUID;{% endif %}

/**
* class {{ className  }}Response 
* 
* @author {{ username  }}
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

    public static {{ className }}Response of({{ className }}Entity entity) {
        return {{ className }}Response.builder()
                {% if isMongo and not isJpa %}.id(entity.getId()){% else %}.id(entity.getId().toString()){% endif %}
                .build();
    }
}
