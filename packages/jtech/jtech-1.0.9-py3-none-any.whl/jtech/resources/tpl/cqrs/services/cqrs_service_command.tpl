/*
*  @(#)Create{{ className }}Service.java
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
package {{ package }}.services.commands;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.services.commands.command.Create{{ className }}Command;

import java.util.Optional;

/**
* class Create{{ className }}Service
*
* @author {{ username }}
**/
public interface Create{{ className }}Service {
    Optional<{{className}}Entity> create(Create{{ className }}Command command);
}
