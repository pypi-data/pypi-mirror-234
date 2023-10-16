
/*
*  @(#) Find{{className}}ByIdController.java
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
import {{ package }}.protocols.{{ className }}Response;
import {{ package }}.services.queries.query.Find{{ className }}ByIdQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;
{% if isJpa %}import java.util.UUID;{% endif %}

/**
* class Find{{ className }}ByIdController
* 
* @author {{ username }}
*/
@RestController
@RequestMapping("/v1/{{ project }}s")
@RequiredArgsConstructor
public class Find{{ className }}ByIdController {

    private final {{ className }}Aggregate aggregate;


    @GetMapping("/{id}")
    public ResponseEntity<{{ className }}Response> findById(@PathVariable String id) {
        return Optional.ofNullable(aggregate.findById(new Find{{ className }}ByIdQuery({% if isMongo and not isJpa %}id{% else %}UUID.fromString(id){% endif %})))
                .map({{ className }}Response::of)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}
