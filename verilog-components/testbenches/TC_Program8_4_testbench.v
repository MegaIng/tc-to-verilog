`timescale 10ns / 1ns

module TC_Program8_4_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg [15:0] address;
    wire [7:0] out0;
    wire [7:0] out1;
    wire [7:0] out2;
    wire [7:0] out3;
    
    // dut instantiation
    TC_Program8_4 dut (.clk(clk), .rst(rst), .address(address), .out0(out0), .out1(out1), .out2(out2), .out3(out3));

    // generate clock
    initial begin
        clk = 1'b0;
        forever #1 clk = ~clk;
    end

    // generate reset
    initial begin
        rst = 1'b1;
        #10
        rst = 1'b0;
    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, address=%16b, out0=%8b, out1=%8b, out2=%8b, out3=%8b\n",
                    $time, address, out0, out1, out2, out3);
        
        // generate all input combinations with 200ns delays
		address = 16'b0000_0000_0000_0000;
        #25
        address = 16'b0000_0000_0000_0001;
        #20
        address = 16'b0000_0000_0000_0010;
        #20
        address = 16'b0000_0000_0000_0011;
        #20
        address = 16'b0000_0000_0000_0100;
        #20
        address = 16'b0000_0000_0000_0101;
        #20
        address = 16'b0000_0000_0000_0110;
        #20
        $finish;
    end
endmodule

