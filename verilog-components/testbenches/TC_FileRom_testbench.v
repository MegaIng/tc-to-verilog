`timescale 10ns / 1ns

module TC_FileRom_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg en;
    reg [15:0] address;
    wire [7:0] out;
    
    // dut instantiation
    TC_FileRom dut (.clk(clk), .rst(rst), .en(en), .address(address), .out(out));

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
        $monitor("time=%3d, address=%16b, out=%8b\n",
                    $time, address, out);
        
        // generate all input combinations with 200ns delays
        en = 1'b0;
		address = 16'b0000_0000_0000_0000;
		#5
		en = 1'b1;
        #20
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
    end
endmodule

