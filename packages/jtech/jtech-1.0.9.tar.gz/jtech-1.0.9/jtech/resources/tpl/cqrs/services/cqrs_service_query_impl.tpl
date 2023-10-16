/*
*  @(#)Find{{ className }}ByIdServiceImpl.java
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
package {{ package }}.services.queries.impl;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.repositories.{{ className }}Repository;
import {{ package }}.services.queries.Find{{ className }}ByIdService;
import {{ package }}.services.queries.query.Find{{ className }}ByIdQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

/**
* class Find{{ className }}ByIdServiceImpl
*
* @author {{ username }}
**/
@Service
@RequiredArgsConstructor
public class Find{{ className }}ByIdServiceImpl implements Find{{ className }}ByIdService {

    private final {{ className }}Repository repository;

    @Override
    public {{ className }}Entity findById(Find{{ className }}ByIdQuery query) {
        return repository.findById(query.id())
                .orElseThrow(() -> new IllegalArgumentException("{{ className }} not found!"));
    }
}


