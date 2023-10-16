/*
*  @(#){{ className }}SuiteTests.java
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
package {{ package }};

import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;
import org.junit.platform.suite.api.SuiteDisplayName;

/**
* class {{ className }}SuiteTests
*
* @author {{ username }}
**/
@Suite
@SuiteDisplayName("Suite test application")
@SelectPackages("{{ package }}")
public class {{ className }}SuiteTests {

}
