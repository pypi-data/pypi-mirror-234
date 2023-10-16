/*
 *  @(#){{ className }}Aggregate.java
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
package {{ package }}.aggregate;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.services.commands.command.Create{{ className }}Command;
import {{ package }}.services.queries.query.Find{{ className }}ByIdQuery;

import java.util.Optional;

/**
 * {{ className }}Aggregate
 *
 *  @author {{ username }}
 */
public interface {{ className }}Aggregate {
    Optional<{{ className }}Entity> create(Create{{ className }}Command command);

    {{ className }}Entity findById(Find{{ className }}ByIdQuery query);
}
