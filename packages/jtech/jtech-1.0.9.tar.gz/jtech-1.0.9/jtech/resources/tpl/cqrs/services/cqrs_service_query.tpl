/*
*  @(#)Find{{ className }}ByIdService.java
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
package {{ package }}.services.queries;

import {{ package }}.entities.{{ className }}Entity;
import {{ package }}.services.queries.query.Find{{ className }}ByIdQuery;


/**
* class Find{{ className }}ByIdService
*
* @author {{ username }}
**/
public interface Find{{ className }}ByIdService {
    {{ className }}Entity findById(Find{{ className }}ByIdQuery query);
}

