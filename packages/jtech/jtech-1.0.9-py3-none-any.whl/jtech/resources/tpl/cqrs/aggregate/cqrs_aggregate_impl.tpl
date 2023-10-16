/*
 *  @(#){{ className }}AggregateImpl.java
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
package {{ package }}.aggregate.impl;

import {{ package }}.aggregate.{{ className }}Aggregate;
import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.services.commands.Create{{ className }}Service;
import {{ package }}.services.commands.command.Create{{ className }}Command;
import {{ package }}.services.queries.Find{{ className }}ByIdService;
import {{ package }}.services.queries.query.Find{{ className }}ByIdQuery;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

/**
 * {{ className }}AggregateImpl
 *
 *  @author {{ username }}
 */
@Service
@RequiredArgsConstructor
public class {{ className }}AggregateImpl implements {{ className }}Aggregate {

    private final Create{{ className }}Service create{{ className }}Service;
    private final Find{{ className }}ByIdService findByIdService;

    @Override
    public Optional<{{ className }}Entity> create(Create{{ className }}Command command) {
        return create{{ className }}Service.create(command);
    }

    @Override
    public {{ className }}Entity findById(Find{{ className }}ByIdQuery query) {
        return findByIdService.findById(query);
    }
}
