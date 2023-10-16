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
package {{ package }}.adapters.output.repositories;

import org.springframework.stereotype.Repository;

/**
* class {{ className  }}Repository 
* 
* user {{ username  }} 
*/
@Repository
public interface {{ className }}Repository {
    // extends this interface to JPARepository<{{ className }}Entity, String> or MongoRepository<{{ className }}Entity, String>
}
