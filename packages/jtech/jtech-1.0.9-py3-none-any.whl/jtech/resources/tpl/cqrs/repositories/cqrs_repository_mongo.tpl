/*
*  @(#){{ className }}Repository.java
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
package {{ package }}.repositories;

import org.springframework.stereotype.Repository;
import org.springframework.data.mongodb.repository.MongoRepository;
import {{ package }}.entities.{{ className }}Entity;

/**
* class {{ className  }}Repository 
* 
* @author {{ username  }}
*/
@Repository
public interface {{ className }}Repository extends MongoRepository<{{ className }}Entity, String> {

}
