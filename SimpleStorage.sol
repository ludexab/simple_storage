//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    uint256 public favNo;
    struct Students {
        string name;
        uint256 MatNo;
        string dept;
    }
    Students[] public student;
    mapping(string => uint256) public searchStudentMat;

    function setStruct(
        string memory _name,
        uint256 _MatNo,
        string memory _dept
    ) public {
        student.push(Students({name: _name, MatNo: _MatNo, dept: _dept}));
        searchStudentMat[_name] = _MatNo;
    }

    function storeFavNo(uint256 _favNo) public {
        favNo = _favNo;
    }

    function viewFavNo() public view returns (uint256) {
        return favNo;
    }
}
