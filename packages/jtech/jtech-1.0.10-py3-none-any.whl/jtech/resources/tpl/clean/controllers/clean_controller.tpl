
/*
*  @(#){{className}}Controller.java
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
package {{ package }}.adapters.input.controllers;

import {{ package }}.adapters.input.protocols.{{ className }}Request;
import {{ package }}.application.ports.input.Create{{ className }}InputGateway;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import static {{ package }}.application.core.domains.{{ className }}.of;

/**
* class {{ className }}Controller
* 
* user {{ username }}
*/
@RestController
@RequestMapping("/api/v1/{{ project }}s")
@RequiredArgsConstructor
public class Create{{ className }}Controller {

    private final Create{{ className }}InputGateway create{{ className }}InputGateway;

    @PostMapping
    public ResponseEntity<Void> create(@RequestBody {{ className }}Request request) {
        create{{ className }}InputGateway.create(of(request));
        return ResponseEntity.noContent().build();
     }
 }
