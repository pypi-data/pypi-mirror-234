
/*
*  @(#) Create{{className}}Controller.java
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
import {{ package }}.protocols.{{ className }}Request;
import {{ package }}.protocols.{{ className }}Response;
import {{ package }}.services.commands.command.Create{{ className }}Command;
import {{ package }}.utils.HttpUtils;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
* class Create{{ className }}Controller
* 
* @author {{ username }}
*/
@RestController
@RequestMapping("/v1/{{ project }}s")
@RequiredArgsConstructor
@Tag(name = "Create a new {{ className }}")
public class Create{{ className }}Controller {

    private final {{ className }}Aggregate aggregate;

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    @Operation(summary = "create a new {{ project }}")
    public ResponseEntity<{{ className }}Response> create(@RequestBody {{ className }}Request request) {
        return aggregate.create(Create{{ className }}Command.of(request))
                .map({{ className }}Response::of)
                .map(HttpUtils::CREATED)
                .orElse(ResponseEntity.notFound().build());
    }
 }
