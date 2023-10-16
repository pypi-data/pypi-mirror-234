/*
*  @(#)Create{{ className }}Command.java
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
import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.protocols.{{ className }}Request;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;
{%if isJpa or not isMongo %}import java.util.UUID;{% endif %}

/**
* class {{ className }}
*
* @author {{ username }}
*/
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Create{{ className }}Command implements Serializable {
    private String id;

    public static Create{{ className }}Command of({{ className }}Request request) {
        return Create{{ className }}Command.builder()
                .id(GenId.newId(request.getId()))
                .build();
    }

    public {{ className }}Entity toEntity() {
        return {{ className }}Entity.builder()
                {% if isMongo and not isJpa %}.id(getId()){% else %}.id(UUID.fromString(getId())){% endif %}
                .build();
    }
}

