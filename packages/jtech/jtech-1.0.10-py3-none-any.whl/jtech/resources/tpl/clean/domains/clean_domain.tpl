/*
*  @(#){{ className }}.java
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
package {{ package }}.application.core.domains;

import {{ package }}.adapters.input.protocols.{{ className }}Request;
import {{ package }}.adapters.output.repositories.entities.{{ className }}Entity;
import lombok.*;

import java.util.UUID;
import java.util.List;


/**
* class {{ className  }} 
* 
* user {{ username  }} 
*/
@Getter
@Setter
@Builder
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class {{ className }} {

    private String id;

    public static List<{{ className }}> of(List<{{ className }}Entity> entities) {
        return entities.stream().map({{ className }}::of).toList();
     }

    public {{ className }}Entity toEntity() {
        return {{ className }}Entity.builder()
            .id(UUID.fromString(getId()))
            .build();
     }

    public static {{ className }} of({{ className }}Entity entity) {
        return {{ className }}.builder()
            .id(entity.getId().toString())
            .build();
     }

    public static {{ className }} of({{ className }}Request request) {
        return {{ className }}.builder()
            .id(request.getId())
            .build();
     }
 }
