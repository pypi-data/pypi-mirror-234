/*
*  @(#)Create{{ className }}ServiceImpl.java
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
package {{ package }}.services.commands.impl;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.repositories.{{ className }}Repository;
import {{ package }}.services.commands.Create{{ className }}Service;
import {{ package }}.services.commands.command.Create{{ className }}Command;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;
/**
* class Create{{ className }}ServiceImpl
*
* @author {{ username }}
**/
@Service
@RequiredArgsConstructor
public class Create{{ className }}ServiceImpl implements Create{{ className }}Service {

    private final {{ className }}Repository repository;

    @Override
    public Optional<{{ className }}Entity> create(Create{{ className }}Command command) {
        return Optional.of(repository.save(command.toEntity()));
    }
}


